using PlayItLoud.API.Repositories.Interfaces;

namespace PlayItLoud.API.Services.Interfaces
{
    public interface IUnitOfWork : IDisposable
    {
        Task<int> SaveChangesAsync();
    }
}
