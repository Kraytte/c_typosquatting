# core/domain_checker.py
import socket
from difflib import SequenceMatcher

def levenshtein_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

def is_similar(domain, target, threshold=0.10):
    return levenshtein_ratio(domain, target) >= threshold

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None