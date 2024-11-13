using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Models;

namespace PlayItLoud.API.Data
{
    public class MusicDbContext : DbContext
    {
        public MusicDbContext(DbContextOptions<MusicDbContext> options) : base(options) { }

        public DbSet<Album> Albums { get; set; }
        public DbSet<Artist> Artists { get; set; }
        public DbSet<Genre> Genres { get; set; }
        public DbSet<Track> Tracks { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Configure many-to-many relationship between Album and Artist.
            modelBuilder.Entity<Album>()
                .HasMany(a => a.Artists)
                .WithMany(ar => ar.Albums)
                .UsingEntity<Dictionary<string, object>>(
                    "AlbumArtist",
                    j => j.HasOne<Artist>().WithMany().HasForeignKey("ArtistId").OnDelete(DeleteBehavior.Cascade),
                    j => j.HasOne<Album>().WithMany().HasForeignKey("AlbumId").OnDelete(DeleteBehavior.Cascade));

            // Configure many-to-many relationship between Album and Genre.
            modelBuilder.Entity<Album>()
                .HasMany(a => a.Genres)
                .WithMany(g => g.Albums)
                .UsingEntity<Dictionary<string, object>>(
                    "AlbumGenre",
                    j => j.HasOne<Genre>().WithMany().HasForeignKey("GenreId").OnDelete(DeleteBehavior.Cascade),
                    j => j.HasOne<Album>().WithMany().HasForeignKey("AlbumId").OnDelete(DeleteBehavior.Cascade));

            // Configure one-to-many relationship between Album and Track.
            modelBuilder.Entity<Track>()
                .HasOne(t => t.Album)
                .WithMany(a => a.Tracks)
                .HasForeignKey(t => t.AlbumId);
        }

    }
}
