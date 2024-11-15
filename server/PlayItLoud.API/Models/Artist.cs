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
        [RegularExpression(@"^(?!\s*$).*", ErrorMessage = "Name cannot contain only whitespaces.")]
        public string Name { get; set; }
        public string Picture { get; set; } = "/images/default.png";
        [RegularExpression(@"^(?!\s*$).*", ErrorMessage = "Alias cannot contain only whitespaces.")]
        public string? Alias { get; set; }
        [Required]
        public DateTime StartDate { get; set; }
        public DateTime? EndDate { get; set; }
        [RegularExpression(@"^(?!\s*$).*", ErrorMessage = "Description cannot contain only whitespaces.")]
        public string? Description { get; set; }
        public ICollection<Album> Albums { get; set; } = new List<Album>();
    }
}
