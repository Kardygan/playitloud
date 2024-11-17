import { Album } from "../../albums/models/album";

export interface Artist {
    id: number;
    name: string;
    picture: string;
    alias?: string;
    startDate: Date;
    endDate?: Date;
    description?: string;
    albums: Album[];
  }