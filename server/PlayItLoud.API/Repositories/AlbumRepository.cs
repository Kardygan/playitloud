using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Data;
using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories
{
    public class AlbumRepository : IAlbumRepository
    {
        private readonly MusicDbContext _context;

        private AlbumRepository(MusicDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Album>> GetAllAsync()
        {
            return await _context.Albums.ToListAsync();
        }

        public async Task<Album?> GetByIdAsync(int id)
        {
            return await _context.Albums.FindAsync(id);
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
