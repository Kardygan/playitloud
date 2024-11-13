using Microsoft.AspNetCore.Mvc;

namespace PlayItLoud.API.Controllers
{
    public class AlbumController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
