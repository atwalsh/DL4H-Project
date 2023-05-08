# DL4H-Project

---

## About

This project contains source code for fully replicating [MIMIC-Extract](https://arxiv.org/abs/1907.08322).

**Project structure**

```bash
.
│   # Copy of MIT-LCP/mimic-code
├── mimic-code
│   # Customized version of MIMIC-Extract
├── MIMIC_Extract
│  ├── ...
│   # Script to easily set up and run MIMIC-Extract database resources
├── mimic_ez.py
│   # Sample outputs from MIMIC-Extract
├── output
│      # Default settings with population size of 25
│  ├── population-25 
│      # Default settings with population size of 1000
│  ├── population-1000 
│      # Ablated data, skipping unit conversion with population size of 1000
│  └── population-1000-no-unit-conversion 
└── README.md
```

Note: `.h5` and `.npy` output files are tracked with Git LFS.

## Resources
- [MIT-LCP/mimic-code](https://github.com/MIT-LCP/mimic-code) -> MIMIC Code Repository: Code shared by the research community for the MIMIC family of databases.
- [atwalsh/MIMIC_Extract](https://github.com/atwalsh/MIMIC_Extract) -> A Data Extraction, Preprocessing, and Representation Pipeline for MIMIC-III. Customized for this application.
- [MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/) via PhysioNet.


## Instructions

This repository provides two methods of configuring your local environment for running MIMIC-Extract:

1. Using the `mimic_ez.py` script to automatically run all necessary steps to build the MIMIC-III database and configure MIMIC_Extract
2. Following the below instructions to build MIMIC-III and configure MIMIC_Extract manually

Both require that you have downloaded the [MIMIC-III Clinical Database](https://physionet.org/content/mimiciii/1.4/), which requires the following steps:

1. Register for an account on the PhysioNet website, which hosts the MIMIC-III database.
2. Become a credentialed user on PhysioNet.
3. Complete the CITI Program training in human subjects research and HIPAA privacy rules.
4. Sign the data use agreement (DUA) form for the dataset.

## Dependencies

Before following either method to configure MIMIC_Extract, you must have the following dependencies installed:

- [PostgreSQL](https://www.postgresql.org/download/)
- [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Computational requirements

- The mimic-code repository suggests that users should reserve 100 GB of space for the PostgreSQL database. It will also likely take many (6+) hours to build the database.
- While users may download individual files of the mimic-code repository, the MIMIC-Extract codebase expects to take full-database. Therefore, users who wish to partially download the dataset should take caution for possible sources of error. 
- Downloading the full ZIP file from PhysioNet may take an hour or more.
- The MIMIC-Extract function may take between 1.5-2 hours to run on the full population in this test case. Running with a smaller population (e.g., 25) only takes a few minutes.

## Accessing the MIMIC-III database

Gain access to the MIMIC-III Clinical Database on PhysioNet:

1. Register for an account on the [PhysioNet website](https://physionet.org/), which hosts the MIMIC-III database.
2. Become a credentialed user on PhysioNet.
3. [Complete the CITI Program training](https://physionet.org/about/citi-course/) in human subjects research and HIPAA privacy rules.
4. Sign the data use agreement (DUA) form for the dataset (at the bottom of the MIMIC-III PhsyioNet page).
5. Download the ZIP file for the MIMIC-III Clinical Database (~6.2 GB in size).

---

## Build for MIMIC-Extract

The below steps outline how to successfully build MIMIC-III and run the MIMIC-Extract program. This was tested on a 2021 MacBook Pro with an Apple M1 Max and 64 GB of RAM, using PostgreSQL 13.5.

### Option 1: Using `mimic_ez.py`

1. Clone this repository with submodules initialized
3. Install dependencies and create conda environment:
	1. Run `export MACOSX_DEPLOYMENT_TARGET=10.9`
	2. Run `conda env create --force -f ./MIMIC_Extract/mimic_extract_env_py36.yml`
3. Run the `mimic_ez.py` script:

```console
python mimic_ez.py \
	--mimic_zip_path $UNZIPPED_MIMIC_DATABASE_DIR \
	--mimic_code_path $CLONED_MIMIC_CODE_DIR \
	--mimic_extract_path $CLONED_MIMIC_EXTRACT_DIR \
	--pg_host localhost \
	--pg_user postgres \
	--pg_password postgres \
	--pg_port 5432 \
	--pg_db mimicez \
```

4. Change directory to `$CLONED_MIMIC_EXTRACT_DIR` and run `python mimic_direct_extract.py`

### Option 2: Building manually

#### 1. Build MIMIC-III

1. Clone [mimic-code](https://github.com/MIT-LCP/mimic-code)
2. Configure a new PostgreSQL database with the name  `mimic`
3. Follow the steps in mimic-code to [create MIMIC-III in a local Postgres database](https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/buildmimic/postgres/README.md)
	1. Unzip the MIMIC-III database
	2. Open `mimic-code/mimic-iii/buildmimic/postgres/` in Terminal
	3. Run `make create-user mimic-gz datadir="/path/to/mimic/zip/"`
		1. NOTE: This will likely take many (6+) hours to complete
		2. By default, the Makefile uses the following parameters:
			-   Database name: `mimic`
			-   User name: `postgres`
			-   Password: `postgres`
			-   Schema: `mimiciii`
			-   Host: none (defaults to localhost)
			-   Port: none (defaults to 5432)
4. Follow the steps in mimic-code to [generate concepts in PostgreSQL](https://github.com/MIT-LCP/mimic-code/blob/main/mimic-iii/concepts/README.md#generating-the-concepts-in-bigquery)
	1. Change directory to `mimic-code/mimic-iii/concepts_postgres/`
	2. Run `psql -d mimic`
	3. Run `SET search_path TO mimiciii;`
	4. Run `\i postgres-functions.sql`
	5. Run `\i postgres-make-concepts.sql`
	6. Exist the database with `\q`


#### 2. Run MIMIC-Extract

1. Clone  [MIMIC-Extract](https://github.com/atwalsh/MIMIC_Extract)
2. Create the Conda environment (See [updated Conda .yml in atwalsh/MIMIC-Extract](https://github.com/atwalsh/MIMIC_Extract/blob/project-draft/mimic_extract_env_py36.yml))
	1. Open the cloned `MIMIC_Extract/utils/` folder in Terminal
	2. Run `export MACOSX_DEPLOYMENT_TARGET=10.9`
	3. Run `conda env create --force -f ../mimic_extract_env_py36.yml`
	4. Activate the environment with `conda activate mimic_data_extraction`
	5. Install the english language model for spacy: `python -m spacy download en_core_web_sm`
3. Build additional MIMIC-Extract concepts in PostgreSQL
	1. Run `bash postgres_make_extended_concepts.sh`
	2. Run `psql -d mimic`
	3. Run `\i niv-durations.sql`
4. Run the extraction script with `python mimic_direct_extract.py`
	1. Set the `--out-path` parameter to the desired extraction output location
	2. Set the `--pop_size` parameter to set a population size 


## References

- Original MIMIC-Extract repository: https://github.com/MLforHealth/MIMIC_Extract
- Original mimic-code repository: https://github.com/MIT-LCP/mimic-code


Shirly Wang, Matthew B. A. McDermott, Geeticka Chauhan, Michael C. * Hughes, Tristan Naumann, and Marzyeh Ghassemi. MIMIC-Extract: A Data Extraction, Preprocessing, and Representation Pipeline for MIMIC-III. arXiv:1907.08322.