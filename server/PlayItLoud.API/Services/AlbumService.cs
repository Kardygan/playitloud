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
                Description = albumDto.Description,
                Label = albumDto.Label
            };

            await AddArtistsToAlbumAsync(albumDto, album);
            await AddGenresToAlbumAsync(albumDto, album);
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
            existingAlbum.Description = albumDto.Description;
            existingAlbum.Label = albumDto.Label;

            existingAlbum.Artists.Clear();
            await AddArtistsToAlbumAsync(albumDto, existingAlbum);

            existingAlbum.Genres.Clear();
            await AddGenresToAlbumAsync(albumDto, existingAlbum);

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

        private async Task AddArtistsToAlbumAsync(AlbumDTO albumDto, Album album)
        {
            foreach (var artistId in albumDto.ArtistIds)
            {
                var artist = await _artistRepository.GetByIdAsync(artistId) ?? throw new EntityNotFoundException($"Artist with id {artistId} not found.");
                album.Artists.Add(artist);
            }
        }

        private async Task AddGenresToAlbumAsync(AlbumDTO albumDto, Album album)
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
                    Duration = trackDto.Duration,
                    Album = album
                });
            }
        }
    }
}
