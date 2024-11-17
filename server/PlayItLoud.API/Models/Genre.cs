using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PlayItLoud.API.Models
{
    [Table("Genre")]
    public class Genre
    {
        public int Id { get; private set; }

        [Required]
        [StringLength(50)]
        public string Name { get; set; }

        public ICollection<Album> Albums { get; set; } = new List<Album>();
    }
}
