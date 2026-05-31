import numpy as np 
import umap

def compute_umap_points(embeddings_candidate, embeddings_job, n_neighbors=15, min_dist=0.1, n_components=2):
    """
        Uniform Manifold Approximation and Projection ofr Dimensioan Reduction
        https://umap-learn.readthedocs.io/en/latest/

        n_neighbors: float - larger values result in more global views of the manifold, while smaller values result in more local data being preserved

        min_dist: float - the effective minimum distance between embedded points. Smaller values will result in a more clustered/clumped embedding where nearby points on the manifold are drawn closer together

        n_components: int - the dimension
    """
    reducer = umap.UMAP(
        n_components=n_components, 
        n_neighbors=n_neighbors, 
        min_dist=min_dist
    )

    all_points = reducer.fit_transform(np.vstack([embeddings_candidate, embeddings_job]))
    
    return {
        "candidate_points": [point.tolist() for point in all_points[:len(embeddings_candidate)]],
        "job_points": [point.tolist() for point in all_points[len(embeddings_candidate):]]
    }