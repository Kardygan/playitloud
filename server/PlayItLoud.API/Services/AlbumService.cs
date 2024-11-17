using PlayItLoud.API.Infrastructure.Exceptions;
using PlayItLoud.API.Models;
using PlayItLoud.API.Models.DTOs;
using PlayItLoud.API.Repositories.Interfaces;
using PlayItLoud.API.Services.Interfaces;

namespace PlayItLoud.API.Services
{
    public class AlbumService : IAlbumService
    {
        private readonly IAlbumRepository _albumRepository;
        private readonly IArtistRepository _artistRepository;
        private readonly IGenreRepository _genreRepository;
        private readonly IUnitOfWork _unitOfWork;

        public AlbumService(IAlbumRepository albumRepository, IArtistRepository artistRepository, IGenreRepository genreRepository, IUnitOfWork unitOfWork)
        {
            _albumRepository = albumRepository;
            _artistRepository = artistRepository;
            _genreRepository = genreRepository;
            _unitOfWork = unitOfWork;
        }

        public async Task<IEnumerable<Album>> GetAllAsync()
        {
            return await _albumRepository.GetAllAsync();
        }

        public async Task<Album?> GetByIdAsync(int id)
        {
            return await _albumRepository.GetByIdAsync(id) ?? throw new EntityNotFoundException($"Album with id {id} not found.");
        }

        public async Task AddAsync(AlbumDTO albumDto)
        {
            EnsureUniqueIds(albumDto);

            var album = new Album
            {
                Name = albumDto.Name,
                ReleaseDate = albumDto.ReleaseDate,
                Description = string.IsNullOrWhiteSpace(albumDto.Description) ? null : albumDto.Description,
                Label = string.IsNullOrWhiteSpace(albumDto.Label) ? null : albumDto.Label
            };

            await AddArtistsToAlbum(albumDto, album);
            await AddGenresToAlbum(albumDto, album);
            AddTracksToAlbum(albumDto, album);

            _albumRepository.Add(album);

            await _unitOfWork.SaveChangesAsync();
        }

        public async Task UpdateAsync(int id, AlbumDTO albumDto)
        {
            EnsureUniqueIds(albumDto);

            var existingAlbum = await _albumRepository.GetByIdAsync(id) ?? throw new EntityNotFoundException($"Album with id {id} not found.");
            existingAlbum.Name = albumDto.Name;
            existingAlbum.ReleaseDate = albumDto.ReleaseDate;
            existingAlbum.Description = string.IsNullOrWhiteSpace(albumDto.Description) ? null : albumDto.Description;
            existingAlbum.Label = string.IsNullOrWhiteSpace(albumDto.Label) ? null : albumDto.Label;

            existingAlbum.Artists.Clear();
            await AddArtistsToAlbum(albumDto, existingAlbum);

            existingAlbum.Genres.Clear();
            await AddGenresToAlbum(albumDto, existingAlbum);

            existingAlbum.Tracks.Clear();
            AddTracksToAlbum(albumDto, existingAlbum);

            _albumRepository.Update(existingAlbum);

            await _unitOfWork.SaveChangesAsync();
        }

        public async Task RemoveAsync(int id)
        {
            var album = await _albumRepository.GetByIdAsync(id) ?? throw new EntityNotFoundException($"Album with id {id} not found.");
            _albumRepository.Remove(album);

            await _unitOfWork.SaveChangesAsync();
        }

        private void EnsureUniqueIds(AlbumDTO albumDto)
        {
            albumDto.ArtistIds = albumDto.ArtistIds.Distinct().ToList();
            albumDto.GenreIds = albumDto.GenreIds.Distinct().ToList();
        }

        private async Task AddArtistsToAlbum(AlbumDTO albumDto, Album album)
        {
            foreach (var artistId in albumDto.ArtistIds)
            {
                var artist = await _artistRepository.GetByIdAsync(artistId) ?? throw new EntityNotFoundException($"Artist with id {artistId} not found.");
                album.Artists.Add(artist);
            }
        }

        private async Task AddGenresToAlbum(AlbumDTO albumDto, Album album)
        {
            foreach (var genreId in albumDto.GenreIds)
            {
                var genre = await _genreRepository.GetByIdAsync(genreId) ?? throw new EntityNotFoundException($"Genre with id {genreId} not found.");
                album.Genres.Add(genre);
            }
        }

        private void AddTracksToAlbum(AlbumDTO albumDto, Album album)
        {
            foreach (var trackDto in albumDto.Tracks)
            {
                album.Tracks.Add(new Track
                {
                    Name = trackDto.Name,
                    Order = trackDto.Order,
                    Duration = (TimeSpan)trackDto.Duration,
                    Album = album
                });
            }
        }
    }
}
