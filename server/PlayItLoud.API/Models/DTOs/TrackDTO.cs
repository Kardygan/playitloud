using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.DTOs
{
    public class TrackDTO
    {
        [Required(ErrorMessage = "Name is required.")]
        [StringLength(1000, ErrorMessage = "Name cannot exceed 1000 characters.")]
        public string Name { get; set; }
        [Required(ErrorMessage = "Order is required.")]
        public int Order { get; set; }
        [Required(ErrorMessage = "Duration is required.")]
        public TimeSpan Duration { get; set; }
    }
}
