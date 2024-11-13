using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Models;

namespace PlayItLoud.API.Data
{
    public static class DbInitializer
    {
        public static void Initialize(MusicDbContext context)
        {
            if (context.Albums.Any())
            {
                return; // DB has been seeded.
            }

            var genres = new Genre[]
            {
                new Genre { Name = "Rock" },
                new Genre { Name = "Pop" },
                new Genre { Name = "Jazz" }
            };

            context.Genres.AddRange(genres);
            context.SaveChanges();

            var artists = new Artist[]
            {
                new Artist { Name = "John Doe", Picture = "/images/artists/artist1.jpg", Alias = "JD, The Doe", StartDate = new DateTime(1987, 1, 12), Description = "First artist description." },
                new Artist { Name = "Jane Doe", Picture = "/images/artists/artist2.jpg", StartDate = new DateTime(1989, 5, 25) },
                new Artist { Name = "Burlu", Alias = "El Burlito", StartDate = new DateTime(2000, 6, 1) },
                new Artist { Name = "Papa Sigraaf", Picture = "/images/artists/artist4.jpg", Alias = "Not Sigraaf", StartDate = new DateTime(1939, 3, 17), EndDate = new DateTime(2010, 7, 3), Description = "Fourth artist description." }
            };

            context.Artists.AddRange(artists);
            context.SaveChanges();

            var albums = new Album[]
            {
                new Album { Name = "The Best Album Ever", Cover = "/images/albums/album1.jpg", ReleaseDate = new DateTime(1999, 1, 1), Label = "Zizare Records", Description = "First album description." },
                new Album { Name = "El Hoyo", ReleaseDate = new DateTime(2024, 5, 1) },
                new Album { Name = "Jazzy Jazz", Cover = "/images/albums/album3.jpg", ReleaseDate = new DateTime(1961, 10, 1), Label = "Oldies Records", Description = "Third album description." }
            };

            context.Albums.AddRange(albums);
            context.SaveChanges();

            var tracks = new Track[]
            {
                new Track { Name = "Track One", Order = 1, Duration = new TimeSpan(0, 4, 22), AlbumId = 1 },
                new Track { Name = "Track Two", Order = 2, Duration = new TimeSpan(0, 3, 9), AlbumId = 1 },
                new Track { Name = "Track Three", Order = 3, Duration = new TimeSpan(0, 5, 50), AlbumId = 1 },

                new Track { Name = "Track One", Order = 1, Duration = new TimeSpan(0, 1, 20), AlbumId = 2 },
                new Track { Name = "Track Two", Order = 2, Duration = new TimeSpan(0, 2, 53), AlbumId = 2 },

                new Track { Name = "Track One", Order = 1, Duration = new TimeSpan(0, 6, 17), AlbumId = 3 }
            };

            context.Tracks.AddRange(tracks);
            context.SaveChanges();

            albums[0].Artists = new List<Artist> { artists[0], artists[1] };
            albums[1].Artists = new List<Artist> { artists[2] };
            albums[2].Artists = new List<Artist> { artists[3] };

            context.SaveChanges();

            albums[0].Genres = new List<Genre> { genres[0] };
            albums[1].Genres = new List<Genre> { genres[1] };
            albums[2].Genres = new List<Genre> { genres[2] };

            context.SaveChanges();
        }
    }
}
