using PlayItLoud.API.Models;
using PlayItLoud.API.Models.DTOs;

namespace PlayItLoud.API.Services.Interfaces
{
    public interface IAlbumService
    {
        Task<IEnumerable<Album>> GetAllAsync();
        Task<Album?> GetByIdAsync(int id);
        Task<Album> AddAsync(AlbumDTO albumDto);
        Task UpdateAsync(int id, AlbumDTO albumDto);
        Task RemoveAsync(int id);
    }
}
