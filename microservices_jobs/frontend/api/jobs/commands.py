MUTATION_CREATE_JOB = """
mutation CreateJob($input: CreateJobInput) {
  job: CreateJob (input: $input) {
    id
    title
    company {
      id
      name
    }
  } 
}       
"""
MUTATION_CREATE_COMPANY = """
mutation CreateCompany($input: CreateCompanyInput) {
  company: CreateCompany (input: $input) {
    id
    name
    jobs {
      id
      title
    }
  } 
}
"""


QUERY_ALL_JOBS = """
query {
  jobs {
    id
    company {
      name
    }
  }
}
"""

QUERY_JOB_BY_ID = """
query JobQuery($id: ID!) {
    job(id: $id) {
        companyId
        title 
        description
        company {
            name
      } 
    }
}
"""

QUERY_COMPANY_BY_ID = """
query CompanyQuery($id: ID!) {
    company(id: $id) {
        id
        name
        description
        jobs {
            id
            title
        }
    } 
}
"""
