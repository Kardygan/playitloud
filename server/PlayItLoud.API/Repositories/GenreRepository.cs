using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Data;
using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories
{
    public class GenreRepository : IGenreRepository
    {
        private readonly MusicDbContext _context;

        public GenreRepository(MusicDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Genre>> GetAllAsync()
        {
            return await _context.Genres.ToListAsync();
        }

        public async Task<Genre?> GetByIdAsync(int id)
        {
            return await _context.Genres.FindAsync(id);
        }

        public void Add(Genre genre)
        {
            _context.Genres.Add(genre);
        }

        public void Update(Genre genre)
        {
            _context.Genres.Update(genre);
        }

        public void Remove(Genre genre)
        {
            _context.Genres.Remove(genre);
        }
    }
}
