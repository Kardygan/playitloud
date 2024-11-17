import { Artist } from "../../artists/models/artist";
import { Genre } from "../../genres/models/genre";
import { Track, TrackDTO } from "./track";

export interface Album {
    id: number;
    name: string;
    cover: string;
    releaseDate?: Date;
    description?: string;
    label?: string;
    artists: Artist[];
    genres: Genre[];
    tracks: Track[];
  }

  export interface AlbumDTO {
    name: string;
    releaseDate?: Date;
    description?: string;
    label?: string;
    artistIds: number[];
    genreIds: number[];
    tracks: TrackDTO[];
  }