using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PlayItLoud.API.Models
{
    [Table("Track")]
    public class Track
    {
        public int Id { get; private set; }

        [Required]
        [StringLength(1000)]
        public string Name { get; set; }

        [Range(1, int.MaxValue)]
        public int Order { get; set; }

        [Required]
        public TimeSpan Duration { get; set; }

        [Required]
        public int AlbumId { get; set; }

        public Album Album { get; set; }
    }
}
