import logging
import time
import traceback
from typing import Union

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError

from app.core.exceptions import NautixException


logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self.handle_exception(request, exc)
    
    async def handle_exception(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle different types of exceptions"""
        
        if isinstance(exc, NautixException):
            return self.create_error_response(
                status_code=exc.status_code,
                message=exc.message,
                details=exc.details,
                request_id=getattr(request.state, 'request_id', None)
            )
        
        elif isinstance(exc, HTTPException):
            return self.create_error_response(
                status_code=exc.status_code,
                message=exc.detail,
                request_id=getattr(request.state, 'request_id', None)
            )
        
        elif isinstance(exc, RequestValidationError):
            return self.create_error_response(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Validation error",
                details={"validation_errors": exc.errors()},
                request_id=getattr(request.state, 'request_id', None)
            )
        
        elif isinstance(exc, SQLAlchemyError):
            logger.error(f"Database error: {str(exc)}", exc_info=True)
            return self.create_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Database error occurred",
                request_id=getattr(request.state, 'request_id', None)
            )
        
        else:
            logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
            return self.create_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Internal server error",
                request_id=getattr(request.state, 'request_id', None)
            )
    
    def create_error_response(
        self,
        status_code: int,
        message: str,
        details: dict = None,
        request_id: str = None
    ) -> JSONResponse:
        """Create standardized error response"""
        
        error_response = {
            "error": {
                "message": message,
                "status_code": status_code,
                "timestamp": str(int(time.time())),
                "type": self.get_error_type(status_code)
            }
        }
        
        if details:
            error_response["error"]["details"] = details
        
        if request_id:
            error_response["error"]["request_id"] = request_id
        
        return JSONResponse(
            status_code=status_code,
            content=error_response
        )
    
    @staticmethod
    def get_error_type(status_code: int) -> str:
        """Get error type based on status code"""
        if 400 <= status_code < 500:
            return "client_error"
        elif 500 <= status_code < 600:
            return "server_error"
        else:
            return "unknown_error"
