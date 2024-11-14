using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories.Interfaces
{
    public interface ITrackRepository
    {
        Task<IEnumerable<Track>> GetAllAsync();
        Task<Track?> GetByIdAsync(int id);
        void Add(Track track);
        void Update(Track track);
        void Remove(Track track);
    }
}
