using Microsoft.AspNetCore.Mvc;
using PlayItLoud.API.Models.DTOs;
using PlayItLoud.API.Services.Interfaces;

namespace PlayItLoud.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AlbumsController : ControllerBase
    {
        private readonly IAlbumService _albumService;

        public AlbumsController(IAlbumService albumService)
        {
            _albumService = albumService;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetAlbum(int id)
        {
            return Ok(await _albumService.GetByIdAsync(id));
        }

        [HttpPost]
        public async Task<IActionResult> PostAlbum([FromBody] AlbumDTO albumDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest();
            }

            await _albumService.AddAsync(albumDto);

            return Ok("Album successfully added.");
        }
    }
}
