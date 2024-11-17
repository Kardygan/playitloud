using System.Collections;
using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.Validators
{
    public class NotEmptyAttribute : ValidationAttribute
    {
        protected override ValidationResult? IsValid(object? value, ValidationContext validationContext)
        {
            if (value is ICollection collection && collection.Count > 0)
            {
                
                return ValidationResult.Success;
            }

            return new ValidationResult(ErrorMessage ?? "The collection must contain at least one element.");
        }
    }
}
