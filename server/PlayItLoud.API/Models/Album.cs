using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PlayItLoud.API.Models
{
    [Table("Album")]
    public class Album
    {
        public int Id { get; private set; }
        [Required]
        [StringLength(1000)]
        public string Name { get; set; }
        public string Cover { get; set; } = "/images/default.png";
        public DateTime? ReleaseDate { get; set; }
        public string? Description { get; set; }
        public string? Label { get; set; }
        public ICollection<Artist> Artists { get; set; } = new List<Artist>();
        public ICollection<Genre> Genres { get; set; } = new List<Genre>();
        public ICollection<Track> Tracks { get; set; } = new List<Track>();
    }
}
