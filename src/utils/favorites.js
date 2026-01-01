// Favorites utility functions using localStorage

const FAVORITES_KEY = 'nba_favorites';

export const getFavorites = () => {
  try {
    const favorites = localStorage.getItem(FAVORITES_KEY);
    return favorites ? JSON.parse(favorites) : [];
  } catch (error) {
    console.error('Error getting favorites:', error);
    return [];
  }
};

export const addFavorite = (player) => {
  try {
    const favorites = getFavorites();
    // Check if player already exists (by player id)
    if (!favorites.find(fav => fav.id === player.id)) {
      favorites.push(player);
      localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
      return true;
    }
    return false;
  } catch (error) {
    console.error('Error adding favorite:', error);
    return false;
  }
};

export const removeFavorite = (playerId) => {
  try {
    const favorites = getFavorites();
    const updated = favorites.filter(fav => fav.id !== playerId);
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(updated));
    return true;
  } catch (error) {
    console.error('Error removing favorite:', error);
    return false;
  }
};

export const isFavorite = (playerId) => {
  try {
    const favorites = getFavorites();
    return favorites.some(fav => fav.id === playerId);
  } catch (error) {
    console.error('Error checking favorite:', error);
    return false;
  }
};

export const toggleFavorite = (player) => {
  if (isFavorite(player.id)) {
    removeFavorite(player.id);
    return false;
  } else {
    addFavorite(player);
    return true;
  }
};

