using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories.Interfaces
{
    public interface IAlbumRepository
    {
        Task<IEnumerable<Album>> GetAllAsync();
        Task<Album?> GetByIdAsync(int id);
        void Add(Album album);
        void Update(Album album);
        void Remove(Album album);
    }
}
