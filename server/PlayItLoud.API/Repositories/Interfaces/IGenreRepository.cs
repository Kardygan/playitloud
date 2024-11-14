using PlayItLoud.API.Models;

namespace PlayItLoud.API.Repositories.Interfaces
{
    public interface IGenreRepository
    {
        Task<IEnumerable<Genre>> GetAllAsync();
        Task<Genre?> GetByIdAsync(int id);
        void Add(Genre genre);
        void Update(Genre genre);
        void Remove(Genre genre);
    }
}
