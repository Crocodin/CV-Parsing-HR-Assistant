import { DeckGL } from '@deck.gl/react';
import { ScatterplotLayer } from '@deck.gl/layers';
import { OrthographicView } from '@deck.gl/core';
import './EmbeddingCanvas.scss';
import type { CVPoint2D } from '../model/CVPoint2D';
import type { JobPoint2D } from '../model/JobPoint2D';

type EmbeddingCordonates = {
  x: number;
  y: number;
  type: 'cv' | 'job';
};

interface Props {
  data: EmbeddingCordonates[];
  setSelectedPoint: (point: JobPoint2D | CVPoint2D | null) => void;
}

function EmbeddingCanvas({ data, setSelectedPoint }: Props) {
  const layer = new ScatterplotLayer({
    id: 'CVs-and-JDs',
    data: data,
    getPosition: (d: EmbeddingCordonates) => [d.x, d.y],
    getRadius: 1,
    getFillColor: (d: EmbeddingCordonates) => {
      return d.type === 'cv' ? [183, 189, 247] : [255, 116, 68];
    },
    onClick: (info) => {
      if (info.object) {
        setSelectedPoint(info.object);
      } else {
        setSelectedPoint(null);
      }
    },
    pickable: true,
  });

  return (
    <div className="embedding-canvas">
      <div className="deck-wrapper rounded-lg">
        <DeckGL
          views={new OrthographicView( {id: 'ortho', controller: true} )}
          initialViewState={{
            target: [0, 0, 0],
            zoom: 1,
          }}
          controller={ true }
          layers={[layer]}
        />
      </div>
    </div>
  );
}

export default EmbeddingCanvas;