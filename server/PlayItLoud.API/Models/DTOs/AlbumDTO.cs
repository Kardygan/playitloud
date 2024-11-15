namespace PlayItLoud.API.Models.DTOs
{
    public class AlbumDTO
    {
        public string Name { get; set; }
        public DateTime? ReleaseDate { get; set; }
        public string? Description { get; set; }
        public string? Label { get; set; }
        public ICollection<int> ArtistIds { get; set; } = new List<int>();
        public ICollection<int> GenreIds { get; set; } = new List<int>();
        public ICollection<TrackDTO> Tracks { get; set; } = new List<TrackDTO>();
    }
}
