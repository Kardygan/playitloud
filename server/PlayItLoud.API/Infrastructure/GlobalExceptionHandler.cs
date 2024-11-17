using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using PlayItLoud.API.Infrastructure.Exceptions;
using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Infrastructure
{
    public class GlobalExceptionHandler : IExceptionHandler
    {
        private readonly ILogger<GlobalExceptionHandler> _logger;

        public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
        {
            _logger = logger;
        }

        public async ValueTask<bool> TryHandleAsync(HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
        {
            _logger.LogError(exception, "Exception occurred: {Message}", exception.Message);

            (int statusCode, string title, string type) = MapExceptionToResponse(exception);
            
            var problemDetails = new ProblemDetails
            {
                Status = statusCode,
                Title = title,
                Type = type,
                Detail = exception.Message
            };

            httpContext.Response.StatusCode = statusCode;

            await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

            return true;
        }

        private (int statusCode, string title, string type) MapExceptionToResponse(Exception exception)
        {
            return exception switch
            {
                ValidationException => (StatusCodes.Status400BadRequest, "Validation Error", "https://datatracker.ietf.org/doc/html/rfc9110#section-15.5.1"),
                UnauthorizedAccessException => (StatusCodes.Status401Unauthorized, "Unauthorized", "https://datatracker.ietf.org/doc/html/rfc9110#section-15.5.2"),
                EntityNotFoundException => (StatusCodes.Status404NotFound, "Not Found", "https://datatracker.ietf.org/doc/html/rfc9110#section-15.5.5"),
                _ => (StatusCodes.Status500InternalServerError, "Internal Server Error", "https://datatracker.ietf.org/doc/html/rfc9110#section-15.6.1")
            };
        }
    }
}
