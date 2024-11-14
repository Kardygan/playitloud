using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories.Interfaces
{
    public interface IArtistRepository
    {
        Task<IEnumerable<Artist>> GetAllAsync();
        Task<Artist?> GetByIdAsync(int id);
        void Add(Artist artist);
        void Update(Artist artist);
        void Remove(Artist artist);
    }
}
