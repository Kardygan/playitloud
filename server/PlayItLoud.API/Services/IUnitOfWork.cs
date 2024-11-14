using PlayItLoud.API.Repositories.Interfaces;

namespace PlayItLoud.API.Services
{
    public interface IUnitOfWork : IDisposable
    {
        Task<int> SaveChangesAsync();
    }
}
