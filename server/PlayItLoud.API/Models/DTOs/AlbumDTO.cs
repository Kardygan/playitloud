using PlayItLoud.API.Models.Validators;
using System.ComponentModel.DataAnnotations;

namespace PlayItLoud.API.Models.DTOs
{
    public class AlbumDTO
    {
        [Required(ErrorMessage = "Album name is required.")]
        [StringLength(1000, MinimumLength = 1, ErrorMessage = "Album name must be between 1 and 1000 characters.")]
        public string Name { get; set; }

        public DateTime? ReleaseDate { get; set; }

        public string? Description { get; set; }

        public string? Label { get; set; }

        [NotEmpty(ErrorMessage = "An album must have at least one artist id.")]
        public ICollection<int> ArtistIds { get; set; } = new List<int>();

        [NotEmpty(ErrorMessage = "An album must have at least one genre id.")]
        public ICollection<int> GenreIds { get; set; } = new List<int>();

        [NotEmpty(ErrorMessage = "An album must have at least one track.")]
        [UniqueOrderNumbers(ErrorMessage = "Track order numbers must be unique.")]
        public ICollection<TrackDTO> Tracks { get; set; } = new List<TrackDTO>();
    }
}
