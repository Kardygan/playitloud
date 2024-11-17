using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.DTOs
{
    public class TrackDTO
    {
        [Required(ErrorMessage = "Track name is required.")]
        [StringLength(1000, MinimumLength = 1, ErrorMessage = "Track name must be between 1 and 1000 characters.")]
        public string Name { get; set; }

        [Range(1, int.MaxValue, ErrorMessage = "Valid track order is required.")]
        public int Order { get; set; }

        [Required(ErrorMessage = "Track duration is required.")]
        public TimeSpan? Duration { get; set; }
    }
}
