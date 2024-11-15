namespace PlayItLoud.API.Models.DTOs
{
    public class TrackDTO
    {
        public string Name { get; set; }
        public int Order { get; set; }
        public TimeSpan Duration { get; set; }
    }
}
