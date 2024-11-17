using PlayItLoud.API.Models.DTOs;
using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.Validators
{
    public class UniqueOrderNumbersAttribute : ValidationAttribute
    {
        protected override ValidationResult? IsValid(object? value, ValidationContext validationContext)
        {
            if (value is ICollection<TrackDTO> tracks)
            {
                var duplicateOrderNumbers = tracks.GroupBy(t => t.Order)
                                                  .Where(g => g.Count() > 1)
                                                  .Select(g => g.Key)
                                                  .ToList();

                if (duplicateOrderNumbers.Count != 0)
                {
                    return new ValidationResult(ErrorMessage ?? "Track order numbers must be unique.");
                }
            }

            return ValidationResult.Success;
        }
    }
}
