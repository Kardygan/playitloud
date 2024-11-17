using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Data;
using PlayItLoud.API.Models;
using PlayItLoud.API.Repositories.Interfaces;

namespace PlayItLoud.API.Repositories
{
    public class AlbumRepository : IAlbumRepository
    {
        private readonly MusicDbContext _context;

        public AlbumRepository(MusicDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Album>> GetAllAsync()
        {
            return await _context.Albums.ToListAsync();
        }

        public async Task<Album?> GetByIdAsync(int id)
        {
            return await _context.Albums
                .Include(a => a.Artists)
                .Include(a => a.Genres)
                .Include(a => a.Tracks)
                .FirstOrDefaultAsync(a => a.Id == id);
        }

        public void Add(Album album)
        {
            _context.Albums.Add(album);
        }

        public void Update(Album album)
        {
            _context.Albums.Update(album);
        }

        public void Remove(Album album)
        {
            _context.Albums.Remove(album);
        }
    }
}
