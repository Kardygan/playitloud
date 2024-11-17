using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PlayItLoud.API.Models
{
    [Table("Artist")]
    public class Artist
    {
        public int Id { get; private set; }
        [Required]
        [StringLength(50)]
        public string Name { get; set; }
        public string Picture { get; set; } = "/images/default.png";
        public string? Alias { get; set; }
        [Required]
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        public string? Description { get; set; }
        public ICollection<Album> Albums { get; set; } = new List<Album>();
    }
}
