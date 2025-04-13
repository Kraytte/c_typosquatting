# core/domain_checker.py
import socket
from difflib import SequenceMatcher

def levenshtein_ratio(a, b):
    """
    Calcule le ratio de similarité entre deux chaînes en utilisant SequenceMatcher.
    Ce ratio varie de 0.0 (aucune similarité) à 1.0 (identiques).
    """
    return SequenceMatcher(None, a, b).ratio()

def is_similar(domain, target, threshold=0.75):
    """
    Détermine si un domaine est similaire à un domaine cible en utilisant un seuil.
    
    Args:
        domain (str): Domaine à analyser (ex: 'g00gle.com').
        target (str): Domaine de référence (ex: 'google.com').
        threshold (float): Seuil de similarité entre 0.0 et 1.0. Plus il est élevé, plus la détection est stricte.
        
    Returns:
        bool: True si le domaine est jugé similaire, sinon False.
    """
    return levenshtein_ratio(domain, target) >= threshold

def resolve_ip(domain):
    """
    Résout un nom de domaine en adresse IPv4 à l'aide d'une requête DNS.
    
    Args:
        domain (str): Le nom de domaine à résoudre.
    
    Returns:
        str | None: Adresse IP correspondante, ou None si la résolution échoue.
    """
    try:
        return socket.gethostbyname(domain)
    except:
        return None