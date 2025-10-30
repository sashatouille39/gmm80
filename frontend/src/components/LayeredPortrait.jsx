import React from 'react';

/**
 * Composant pour afficher un portrait de joueur
 * - Portraits réalistes complets (NOUVEAU) : Si realistic_portrait est disponible
 * - Calques PNG superposés (ANCIEN) : Si les calques sont disponibles
 * - Fallback : Cercle avec numéro
 */
const LayeredPortrait = ({ player, size = 'medium', className = '', showNumber = false }) => {
  // Vérifier si un portrait réaliste est disponible (NOUVEAU SYSTÈME)
  const hasRealisticPortrait = player?.portrait?.realistic_portrait;
  
  // Vérifier si les calques sont disponibles (ANCIEN SYSTÈME)
  const hasLayers = player?.portrait?.layer_base || 
                    player?.portrait?.layer_eyes ||
                    player?.portrait?.layer_hair ||
                    player?.portrait?.layer_mouth ||
                    player?.portrait?.layer_nose;

  // Tailles prédéfinies
  const sizes = {
    tiny: 'w-8 h-8',
    small: 'w-12 h-12',
    medium: 'w-20 h-20',
    large: 'w-32 h-32',
    xlarge: 'w-48 h-48'
  };

  const sizeClass = sizes[size] || sizes.medium;

  // URL backend
  const backendUrl = process.env.REACT_APP_BACKEND_URL || '';

  // PRIORITÉ 1 : Portrait réaliste complet
  if (hasRealisticPortrait) {
    return (
      <div className={`${sizeClass} ${className} relative overflow-hidden rounded-full bg-gray-100`}>
        <img
          src={`${backendUrl}${player.portrait.realistic_portrait}`}
          alt={`Portrait de ${player.name}`}
          className="w-full h-full object-cover"
          onError={(e) => {
            // En cas d'erreur, afficher le fallback
            e.target.style.display = 'none';
            e.target.parentElement.innerHTML = `
              <div class="w-full h-full rounded-full flex items-center justify-center text-white font-bold ${
                player?.alive === false ? 'bg-red-600' : 'bg-blue-600'
              }">
                ${showNumber && player?.number ? player.number : '?'}
              </div>
            `;
          }}
        />
        
        {/* Badge du numéro du joueur (optionnel) */}
        {player?.number && (
          <div className="absolute bottom-0 right-0 bg-black bg-opacity-70 text-white text-xs px-2 py-1 rounded-tl-lg" style={{ zIndex: 10 }}>
            #{player.number}
          </div>
        )}
      </div>
    );
  }

  // PRIORITÉ 2 : Affichage avec calques superposés (ANCIEN SYSTÈME)
  if (hasLayers) {
    return (
      <div className={`${sizeClass} ${className} relative overflow-hidden rounded-full bg-gray-100`}>
        {/* Conteneur pour les calques avec position relative */}
        <div className="relative w-full h-full">
          {/* Calque 1: Base (tête avec peau) */}
          {player.portrait.layer_base && (
            <img
              src={`${backendUrl}${player.portrait.layer_base}`}
              alt="Base"
              className="absolute top-0 left-0 w-full h-full object-contain"
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
              className="absolute top-0 left-0 w-full h-full object-contain"
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
              className="absolute top-0 left-0 w-full h-full object-contain"
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
              className="absolute top-0 left-0 w-full h-full object-contain"
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
              className="absolute top-0 left-0 w-full h-full object-contain"
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
  }

  // PRIORITÉ 3 : Affichage fallback (cercle avec numéro)
  return (
    <div className={`${sizeClass} ${className} relative flex items-center justify-center`}>
      <div 
        className={`w-full h-full rounded-full flex items-center justify-center text-white font-bold ${
          player?.alive === false ? 'bg-red-600' : 'bg-blue-600'
        }`}
        style={{ 
          fontSize: size === 'tiny' ? '0.625rem' : size === 'small' ? '0.75rem' : '1rem'
        }}
      >
        {showNumber && player?.number ? player.number : '?'}
      </div>
    </div>
  );
};

export default LayeredPortrait;
