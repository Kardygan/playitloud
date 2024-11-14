using PlayItLoud.API.Services;

namespace PlayItLoud.API.Data
{
    public class UnitOfWork : IUnitOfWork
    {
        private readonly MusicDbContext _context;

        public UnitOfWork(MusicDbContext context)
        {
            _context = context;
        }

        public async Task<int> SaveChangesAsync()
        {
            return await _context.SaveChangesAsync();
        }

        public void Dispose()
        {
            _context.Dispose();
        }
    }
}
