using PlayItLoud.API.Models.DTOs;
using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.Validators
{
    public class SequentialOrderNumbersAttribute : ValidationAttribute
    {
        protected override ValidationResult? IsValid(object? value, ValidationContext validationContext)
        {
            if (value is ICollection<TrackDTO> tracks && tracks.Count > 0)
            {
                var orderNumbers = tracks.Select(t => t.Order).OrderBy(o => o).ToList();

                if (orderNumbers.First() != 1 || orderNumbers.Where((o, i) => o != i + 1).Any())
                {
                    return new ValidationResult(ErrorMessage ?? "Track order numbers must start at 1 and increment without gaps.");
                }
            }

            return ValidationResult.Success;
        }
    }
}
