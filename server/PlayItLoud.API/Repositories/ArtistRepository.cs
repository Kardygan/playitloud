using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Data;
using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories
{
    public class ArtistRepository : IArtistRepository
    {
        private readonly MusicDbContext _context;

        public ArtistRepository(MusicDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Artist>> GetAllAsync()
        {
            return await _context.Artists.ToListAsync();
        }

        public async Task<Artist?> GetByIdAsync(int id)
        {
            return await _context.Artists.FindAsync(id);
        }

        public void Add(Artist artist)
        {
            _context.Artists.Add(artist);
        }

        public void Update(Artist artist)
        {
            _context.Artists.Update(artist);
        }

        public void Remove(Artist artist)
        {
            _context.Artists.Remove(artist);
        }
    }
}
