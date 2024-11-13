using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace PlayItLoud.API.Migrations
{
    /// <inheritdoc />
    public partial class UpdateAlbumArtistGenreRelationships : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_AlbumArtist_Album_AlbumsId",
                table: "AlbumArtist");

            migrationBuilder.DropForeignKey(
                name: "FK_AlbumArtist_Artist_ArtistsId",
                table: "AlbumArtist");

            migrationBuilder.DropForeignKey(
                name: "FK_AlbumGenre_Album_AlbumsId",
                table: "AlbumGenre");

            migrationBuilder.DropForeignKey(
                name: "FK_AlbumGenre_Genre_GenresId",
                table: "AlbumGenre");

            migrationBuilder.RenameColumn(
                name: "GenresId",
                table: "AlbumGenre",
                newName: "GenreId");

            migrationBuilder.RenameColumn(
                name: "AlbumsId",
                table: "AlbumGenre",
                newName: "AlbumId");

            migrationBuilder.RenameIndex(
                name: "IX_AlbumGenre_GenresId",
                table: "AlbumGenre",
                newName: "IX_AlbumGenre_GenreId");

            migrationBuilder.RenameColumn(
                name: "ArtistsId",
                table: "AlbumArtist",
                newName: "ArtistId");

            migrationBuilder.RenameColumn(
                name: "AlbumsId",
                table: "AlbumArtist",
                newName: "AlbumId");

            migrationBuilder.RenameIndex(
                name: "IX_AlbumArtist_ArtistsId",
                table: "AlbumArtist",
                newName: "IX_AlbumArtist_ArtistId");

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumArtist_Album_AlbumId",
                table: "AlbumArtist",
                column: "AlbumId",
                principalTable: "Album",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumArtist_Artist_ArtistId",
                table: "AlbumArtist",
                column: "ArtistId",
                principalTable: "Artist",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumGenre_Album_AlbumId",
                table: "AlbumGenre",
                column: "AlbumId",
                principalTable: "Album",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumGenre_Genre_GenreId",
                table: "AlbumGenre",
                column: "GenreId",
                principalTable: "Genre",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_AlbumArtist_Album_AlbumId",
                table: "AlbumArtist");

            migrationBuilder.DropForeignKey(
                name: "FK_AlbumArtist_Artist_ArtistId",
                table: "AlbumArtist");

            migrationBuilder.DropForeignKey(
                name: "FK_AlbumGenre_Album_AlbumId",
                table: "AlbumGenre");

            migrationBuilder.DropForeignKey(
                name: "FK_AlbumGenre_Genre_GenreId",
                table: "AlbumGenre");

            migrationBuilder.RenameColumn(
                name: "GenreId",
                table: "AlbumGenre",
                newName: "GenresId");

            migrationBuilder.RenameColumn(
                name: "AlbumId",
                table: "AlbumGenre",
                newName: "AlbumsId");

            migrationBuilder.RenameIndex(
                name: "IX_AlbumGenre_GenreId",
                table: "AlbumGenre",
                newName: "IX_AlbumGenre_GenresId");

            migrationBuilder.RenameColumn(
                name: "ArtistId",
                table: "AlbumArtist",
                newName: "ArtistsId");

            migrationBuilder.RenameColumn(
                name: "AlbumId",
                table: "AlbumArtist",
                newName: "AlbumsId");

            migrationBuilder.RenameIndex(
                name: "IX_AlbumArtist_ArtistId",
                table: "AlbumArtist",
                newName: "IX_AlbumArtist_ArtistsId");

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumArtist_Album_AlbumsId",
                table: "AlbumArtist",
                column: "AlbumsId",
                principalTable: "Album",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumArtist_Artist_ArtistsId",
                table: "AlbumArtist",
                column: "ArtistsId",
                principalTable: "Artist",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumGenre_Album_AlbumsId",
                table: "AlbumGenre",
                column: "AlbumsId",
                principalTable: "Album",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_AlbumGenre_Genre_GenresId",
                table: "AlbumGenre",
                column: "GenresId",
                principalTable: "Genre",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
