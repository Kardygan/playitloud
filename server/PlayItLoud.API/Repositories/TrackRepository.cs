using Microsoft.EntityFrameworkCore;
using PlayItLoud.API.Data;
using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories
{
    public class TrackRepository : ITrackRepository
    {
        private readonly MusicDbContext _context;

        public TrackRepository(MusicDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<Track>> GetAllAsync()
        {
            return await _context.Tracks.ToListAsync();
        }

        public async Task<Track?> GetByIdAsync(int id)
        {
            return await _context.Tracks.FindAsync(id);
        }

        public void Add(Track track)
        {
            _context.Tracks.Add(track);
        }

        public void Update(Track track)
        {
            _context.Tracks.Update(track);
        }

        public void Remove(Track track)
        {
            _context.Tracks.Remove(track);
        }
    }
}
