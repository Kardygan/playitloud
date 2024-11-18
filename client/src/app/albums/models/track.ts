import { Album } from "./album";

export interface Track {
    id: number;
    name: string;
    order: number;
    duration?: string;
    albumId: number;
    album: Album;
}

export interface TrackDTO {
    name: string;
    order: number;
    duration?: string;
}