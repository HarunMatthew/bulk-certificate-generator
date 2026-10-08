from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Job, Certificate
from app.schemas.schemas import JobCreate
from app.services.certificate_service import generate_certificate


router = APIRouter(prefix="/api", tags=["Certificates"])


@router.post("/jobs/")
def create_job(request: JobCreate, db: Session = Depends(get_db)):
    # Create job
    job = Job(
        event_name=request.event_name,
        event_date=request.date,
        status="PROCESSING",
        total=len(request.recipients),
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Create certificate records
    for recipient in request.recipients:
        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=str(recipient.email),
            status="PENDING",
        )

        db.add(certificate)

    db.commit()

    # Generate certificates individually
    certificates = db.query(Certificate).filter(Certificate.job_id == job.id).all()

    for certificate in certificates:
        try:
            file_path = generate_certificate(
                certificate.recipient_name,
                job.event_name,
                job.event_date,
                certificate.id,
            )

            certificate.status = "SUCCESS"
            certificate.file_path = file_path
            job.successful += 1

        except Exception as error:
            certificate.status = "FAILED"
            certificate.error_message = str(error)
            job.failed += 1

    # Update job status
    if job.failed == 0:
        job.status = "COMPLETED"
    else:
        job.status = "COMPLETED_WITH_ERRORS"

    db.commit()
    db.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
    }


@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed,
        "created_at": job.created_at,
    }


@router.get("/jobs/{job_id}/certificates/")
def get_certificates(job_id: int, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    certificates = db.query(Certificate).filter(Certificate.job_id == job_id).all()

    return {
        "job_id": job_id,
        "certificates": [
            {
                "certificate_id": certificate.id,
                "recipient_name": certificate.recipient_name,
                "recipient_email": certificate.recipient_email,
                "status": certificate.status,
                "error": certificate.error_message,
            }
            for certificate in certificates
        ],
    }


@router.get("/certificates/{certificate_id}")
def download_certificate(certificate_id: int, db: Session = Depends(get_db)):
    certificate = db.get(Certificate, certificate_id)

    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    if (
        certificate.status != "SUCCESS"
        or not certificate.file_path
        or not Path(certificate.file_path).exists()
    ):
        raise HTTPException(status_code=404, detail="Certificate file not available")

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=Path(certificate.file_path).name,
    )
