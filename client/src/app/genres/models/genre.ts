import { Album } from "../../albums/models/album";

export interface Genre {
    id: number;
    name: string;
    albums: Album[];
}