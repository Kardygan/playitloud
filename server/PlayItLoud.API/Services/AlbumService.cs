﻿using PlayItLoud.API.Models;
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
            var album = await _albumRepository.GetByIdAsync(id);
            if (album == null)
                throw new KeyNotFoundException($"Album with ID {id} not found.");

            return album;
        }

        public async Task AddAsync(AlbumDTO albumDto)
        {
            var album = new Album
            {
                Name = albumDto.Name,
                ReleaseDate = albumDto.ReleaseDate,
                Description = albumDto.Description,
                Label = albumDto.Label
            };

            foreach (var artistId in albumDto.ArtistIds)
            {
                var artist = await _artistRepository.GetByIdAsync(artistId);
                if (artist == null)
                    throw new Exception($"Artist with ID {artistId} not found.");

                album.Artists.Add(artist);
            }

            foreach (var genreId in albumDto.GenreIds)
            {
                var genre = await _genreRepository.GetByIdAsync(genreId);
                if (genre == null)
                    throw new Exception($"Genre with ID {genreId} not found.");

                album.Genres.Add(genre);
            }

            foreach (var trackDto in albumDto.Tracks)
            {
                var track = new Track
                {
                    Name = trackDto.Name,
                    Order = trackDto.Order,
                    Duration = trackDto.Duration,
                    Album = album
                };

                album.Tracks.Add(track);
            }

            _albumRepository.Add(album);

            await _unitOfWork.SaveChangesAsync();
        }

        public async Task UpdateAsync(int id, AlbumDTO albumDto)
        {
            var existingAlbum = await _albumRepository.GetByIdAsync(id);
            if (existingAlbum == null)
                throw new KeyNotFoundException($"Album with ID {id} not found.");

            existingAlbum.Name = albumDto.Name;
            existingAlbum.ReleaseDate = albumDto.ReleaseDate;
            existingAlbum.Description = albumDto.Description;
            existingAlbum.Label = albumDto.Label;

            existingAlbum.Artists.Clear();
            foreach (var artistId in albumDto.ArtistIds)
            {
                var artist = await _artistRepository.GetByIdAsync(artistId);
                if (artist == null)
                    throw new Exception($"Artist with ID {artistId} not found.");

                existingAlbum.Artists.Add(artist);
            }

            existingAlbum.Genres.Clear();
            foreach (var genreId in albumDto.GenreIds)
            {
                var genre = await _genreRepository.GetByIdAsync(genreId);
                if (genre == null)
                    throw new Exception($"Genre with ID {genreId} not found.");

                existingAlbum.Genres.Add(genre);
            }

            existingAlbum.Tracks.Clear();
            foreach (var trackDto in albumDto.Tracks)
            {
                var track = new Track
                {
                    Name = trackDto.Name,
                    Order = trackDto.Order,
                    Duration = trackDto.Duration,
                    Album = existingAlbum
                };

                existingAlbum.Tracks.Add(track);
            }

            _albumRepository.Update(existingAlbum);

            await _unitOfWork.SaveChangesAsync();
        }

        public async Task RemoveAsync(int id)
        {
            var album = await _albumRepository.GetByIdAsync(id);
            if (album == null)
                throw new KeyNotFoundException($"Album with ID {id} not found.");

            _albumRepository.Remove(album);

            await _unitOfWork.SaveChangesAsync();
        }
    }
}
