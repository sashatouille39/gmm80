import React from 'react';

/**
 * Composant pour afficher un portrait composé de calques PNG superposés
 * Les calques sont générés par IA et cohérents avec la nationalité et le sexe
 */
const LayeredPortrait = ({ player, size = 'medium', className = '' }) => {
  // Si pas de calques disponibles, afficher le portrait simple
  const hasLayers = player?.portrait?.layer_base || 
                    player?.portrait?.layer_eyes ||
                    player?.portrait?.layer_hair ||
                    player?.portrait?.layer_mouth ||
                    player?.portrait?.layer_nose;

  // Tailles prédéfinies
  const sizes = {
    small: 'w-12 h-12',
    medium: 'w-20 h-20',
    large: 'w-32 h-32',
    xlarge: 'w-48 h-48'
  };

  const sizeClass = sizes[size] || sizes.medium;

  // URL backend
  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

  if (!hasLayers) {
    // Affichage fallback avec le style simple
    return (
      <div className={`${sizeClass} ${className} relative`}>
        <div 
          className="w-full h-full rounded-full"
          style={{ backgroundColor: player?.portrait?.skin_color || '#F5CBA7' }}
        >
          {/* Yeux simples */}
          <div className="absolute top-1/3 left-1/4 w-2 h-2 rounded-full bg-gray-800"></div>
          <div className="absolute top-1/3 right-1/4 w-2 h-2 rounded-full bg-gray-800"></div>
          {/* Cheveux simples */}
          <div 
            className="absolute top-0 left-0 w-full h-1/2 rounded-t-full opacity-80"
            style={{ backgroundColor: player?.portrait?.hair_color || '#4A4A4A' }}
          ></div>
        </div>
      </div>
    );
  }

  // Affichage avec calques superposés
  return (
    <div className={`${sizeClass} ${className} relative overflow-hidden`}>
      {/* Conteneur pour les calques avec position relative */}
      <div className="relative w-full h-full">
        {/* Calque 1: Base (tête avec peau) */}
        {player.portrait.layer_base && (
          <img
            src={`${backendUrl}${player.portrait.layer_base}`}
            alt="Base"
            className="absolute top-0 left-0 w-full h-full object-cover"
            style={{ zIndex: 1 }}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        )}

        {/* Calque 2: Nez */}
        {player.portrait.layer_nose && (
          <img
            src={`${backendUrl}${player.portrait.layer_nose}`}
            alt="Nez"
            className="absolute top-0 left-0 w-full h-full object-cover"
            style={{ zIndex: 2 }}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        )}

        {/* Calque 3: Bouche */}
        {player.portrait.layer_mouth && (
          <img
            src={`${backendUrl}${player.portrait.layer_mouth}`}
            alt="Bouche"
            className="absolute top-0 left-0 w-full h-full object-cover"
            style={{ zIndex: 3 }}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        )}

        {/* Calque 4: Yeux */}
        {player.portrait.layer_eyes && (
          <img
            src={`${backendUrl}${player.portrait.layer_eyes}`}
            alt="Yeux"
            className="absolute top-0 left-0 w-full h-full object-cover"
            style={{ zIndex: 4 }}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        )}

        {/* Calque 5: Cheveux (au-dessus de tout) */}
        {player.portrait.layer_hair && (
          <img
            src={`${backendUrl}${player.portrait.layer_hair}`}
            alt="Cheveux"
            className="absolute top-0 left-0 w-full h-full object-cover"
            style={{ zIndex: 5 }}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        )}
      </div>

      {/* Badge du numéro du joueur (optionnel) */}
      {player?.number && (
        <div className="absolute bottom-0 right-0 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded-tl-lg" style={{ zIndex: 10 }}>
          #{player.number}
        </div>
      )}
    </div>
  );
};

export default LayeredPortrait;
