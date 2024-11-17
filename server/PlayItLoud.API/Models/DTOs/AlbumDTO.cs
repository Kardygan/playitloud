using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.DTOs
{
    public class AlbumDTO
    {
        [Required(ErrorMessage = "Name is required.")]
        [StringLength(1000, ErrorMessage = "Name cannot exceed 1000 characters.")]
        public string Name { get; set; }
        public DateTime? ReleaseDate { get; set; }
        public string? Description { get; set; }
        public string? Label { get; set; }
        public ICollection<int> ArtistIds { get; set; } = new List<int>();
        public ICollection<int> GenreIds { get; set; } = new List<int>();
        public ICollection<TrackDTO> Tracks { get; set; } = new List<TrackDTO>();
    }
}
