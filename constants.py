    
import re

#Uses regex word boundaries now
KEYWORDS = re.compile(
    r"\b(intern|co-op|coop|student|internships)\b",
    re.IGNORECASE
)
