from Bio import Entrez

def fetch_species(accession_list):
    Entrez.email = "giuliamagriribeiro@gmail.com"  # Put your email here
    species_list = []

    for accession in accession_list:
        try:
            handle = Entrez.esummary(db="nucleotide", id=accession)
            record = Entrez.read(handle)
            handle.close()
            if 'Title' in record[0]:
                title = record[0]['Title']
                # Extract first two words as species name
                species = " ".join(title.split(",")[0].split()[:2])
                species_list.append((accession, species))
            else:
                print(f"Species not found for accession {accession}")
                species_list.append((accession, "Species not found"))
        except Exception as e:
            print(f"Error fetching accession {accession}: {e}")
            species_list.append((accession, f"Error fetching accession {accession}: {e}"))

    return species_list

def write_species_names(species_list, output_file):
    with open(output_file, "w") as f:
        for accession, species in species_list:
            f.write(accession + "\t" + species + "\n")

def write_results(species_list, output_file):
    with open(output_file, "w") as f:
        for accession, species in species_list:
            f.write(accession + "\t" + species + "\n")

def main():
    # Read accession list from file
    with open("SSU_list.txt", "r") as f:
        accession_list = f.read().splitlines()

    species_list = fetch_species(accession_list)

    # Write species names to file
    write_species_names(species_list, "species_names.txt")

    # Write old output to file
    write_results(species_list, "SSU_species_results.txt")

if __name__ == "__main__":
    main()
