from Bio import Entrez
import time
from http.client import IncompleteRead

def get_taxonomy(species_name):
    Entrez.email = "your@email.com"  # Enter your email here
    handle = Entrez.esearch(db="taxonomy", term=species_name, retmax=1)
    record = Entrez.read(handle)
    if record["IdList"]:
        tax_id = record["IdList"][0]
        for _ in range(3):  # Retry up to 3 times
            try:
                taxonomy = Entrez.efetch(db="taxonomy", id=tax_id, retmode="xml")
                tax_record = Entrez.read(taxonomy)[0]
                lineage = tax_record.get("Lineage", [])
                scientific_name = tax_record.get("ScientificName", "")

                # Check if lineage is a string and convert to list of dictionaries if needed
                if isinstance(lineage, str):
                    lineage = [{"Rank": "species", "ScientificName": lineage}]

                # Create a dictionary for taxonomy
                taxonomy_dict = {}
                for level in lineage:
                    rank = level.get("Rank", "")
                    name = level.get("ScientificName", "")
                    if rank and name:
                        taxonomy_dict[rank] = name

                return scientific_name, taxonomy_dict
            except IncompleteRead as e:
                print("Error occurred:", e)
                print("Retrying...")
                time.sleep(2)  # Add a delay of 2 seconds between retries
            except Exception as e:
                print("Error occurred:", e)
                return None, None
    else:
        return None, None

def process_species_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for species_name in infile:
            species_name = species_name.strip()
            scientific_name, taxonomy = get_taxonomy(species_name)
            if scientific_name is None:
                outfile.write(f"Error retrieving taxonomy for: {species_name}\n")
            else:
                outfile.write("{:<40}\t".format(scientific_name))
                for rank, name in taxonomy.items():
                    outfile.write(rank + ": " + name + "\t")
                outfile.write("\n")

input_file = "species_names.txt"  # Input file containing species names, one per line
output_file = "taxonomy_results.txt"  # Output file to write taxonomy results
process_species_file(input_file, output_file)
