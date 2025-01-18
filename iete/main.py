import json
from typing import Optional

import streamlit as st
from phi.agent import Agent
from phi.tools.file import FileTools
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.calculator import Calculator
from phi.tools.duckdb import DuckDbTools
from phi.tools.googlesearch import GoogleSearch
from phi.tools.pandas import PandasTools
from phi.utils.log import logger

# Initialize Agents

document_parser = Agent(
    tools=[FileTools()],
    instructions=[
        "Parse uploaded documents for structured financial, tax, or user-provided queries. Extract key information."
    ],
)

tax_knowledge = Agent(
    tools=[DuckDuckGo()],
    instructions=[
        "Search the web to provide the latest tax rules and exemptions. Include references for credibility."
    ],
)

content_optimizer = Agent(
    tools=[DuckDuckGo(), GoogleSearch()],
    instructions=[
        "Assist content creators with tips for managing taxes on irregular income streams. Offer deductions and optimization strategies."
    ],
)

financial_planner = Agent(
    tools=[Calculator(), DuckDbTools()],
    instructions=[
        "Assist with financial planning by analyzing income, expenses, and savings. Provide budgets or investment strategies."
    ],
)

business_tax_optimizer = Agent(
    tools=[DuckDuckGo(), Calculator()],
    instructions=[
        "Help business owners optimize their taxes by identifying eligible deductions, investment strategies, and compliance with tax regulations."
    ],
)

irregular_income_advisor = Agent(
    tools=[DuckDuckGo(), GoogleSearch()],
    instructions=[
        "Provide personalized tax optimization strategies for individuals with irregular income streams, such as freelancers or gig workers."
    ],
)

investment_advisor = Agent(
    tools=[DuckDuckGo(), Calculator()],
    instructions=[
        "Recommend tax-saving investment options such as ELSS, PPF, and NPS. Provide insights into their financial benefits and risks."
    ],
)

compliance_checker = Agent(
    tools=[FileTools()],
    instructions=[
        "Review uploaded financial and tax documents to ensure compliance with regulatory requirements. Highlight any missing or inconsistent information."
    ],
)

reporting_agent = Agent(
    tools=[PandasTools()],
    instructions=[
        "Generate professional, visually appealing reports with charts and summaries based on the analysis."
    ],
)


def main():
    st.set_page_config(page_title="GenZ AI Tax Optimization Assistant", layout="wide")

    # Custom Style
    st.markdown(
        """
        <style>
        .main {background-color: #1e1e1e; color: #dcdcdc;}
        .stButton > button {background-color: #007ACC; color: white; border: none; padding: 10px 20px; border-radius: 5px;}
        .stTextInput > div > input {background-color: #2d2d2d; color: #dcdcdc; border: none; border-radius: 5px;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("GenZ AI Tax Optimization Assistant")
    st.markdown(
        """
        Welcome to the **GenZ AI-powered assistant**, designed to help content creators, business owners, and individuals 
        manage their taxes, finances, and investments efficiently. Explore the features below and get started!
        """
    )

    # Add Sections in the Right Area
    st.subheader("🎯 Key Features")
    st.markdown(
        """
        - **Tax Knowledge**: Get the latest updates on tax laws and exemptions.
        - **Content Optimization**: Tailored advice for managing irregular income streams.
        - **Financial Planning**: Analyze your finances and create effective strategies.
        - **Business Tax Optimization**: Maximize savings for businesses with expert tips.
        - **Investment Insights**: Explore tax-saving investments with comprehensive insights.
        """
    )

    st.subheader("💡 Pro Tips")
    st.markdown(
        """
        - Keep track of your income and expenses regularly for better tax management.
        - Utilize deductions like **Section 80C** for maximum tax savings.
        - For freelancers: Separate personal and professional expenses for better tracking.
        """
    )

    st.subheader("📅 Recent Updates")
    st.markdown(
        """
        - **March 31, 2025**: Deadline for filing revised or belated income tax returns.
        - **April 2025**: New tax slabs introduced for FY 2024-25.
        """
    )

    st.sidebar.header("Quick Options")
    st.sidebar.markdown("Select a query type or upload a document to begin.")

    st.sidebar.markdown("**Key Query Terms:**")
    st.sidebar.markdown(
        """
        - **tax**: For tax knowledge and exemptions.
        - **content**: For content optimization and irregular income.
        - **financial**: For financial planning.
        - **business**: For business tax optimization.
        - **irregular**: For advising on irregular income streams.
        - **investment**: For tax-saving investment advice.
        - **compliance**: For checking document compliance.
        - **report**: For generating detailed reports.
        """
    )

    # File upload
    st.sidebar.subheader("Document Upload")
    document = st.sidebar.file_uploader(
        "Upload a document (PDF, CSV, etc.)", type=["pdf", "csv"]
    )

    if document:
        with st.spinner("Parsing document..."):
            parsed_data = document_parser.run(document.read()).content
        st.success("Document parsed successfully!")
        st.json(parsed_data)

    # User query input
    st.sidebar.subheader("Ask a Query")
    user_query = st.sidebar.text_input(
        "Enter your query (e.g., tax advice, financial planning, content optimization)"
    )

    if st.sidebar.button("Submit Query"):
        st.subheader("Query Results")
        if "tax" in user_query.lower():
            with st.spinner("Fetching tax knowledge..."):
                tax_response = tax_knowledge.run(user_query)
            st.write("### Tax Knowledge Response:")
            st.write(tax_response.content)

        elif "content" in user_query.lower():
            with st.spinner("Analyzing content optimization..."):
                content_response = content_optimizer.run(user_query)
            st.write("### Content Optimization Response:")
            st.write(content_response.content)

        elif "financial" in user_query.lower():
            with st.spinner("Generating financial plan..."):
                financial_response = financial_planner.run({})
            st.write("### Financial Planning Response:")
            st.write(financial_response.content)

        elif "business" in user_query.lower():
            with st.spinner("Optimizing business taxes..."):
                business_response = business_tax_optimizer.run(user_query)
            st.write("### Business Tax Optimization Response:")
            st.write(business_response.content)

        elif "irregular" in user_query.lower():
            with st.spinner("Advising on irregular income..."):
                irregular_income_response = irregular_income_advisor.run(user_query)
            st.write("### Irregular Income Advisor Response:")
            st.write(irregular_income_response.content)

        elif "investment" in user_query.lower():
            with st.spinner("Advising on tax-saving investments..."):
                investment_response = investment_advisor.run(user_query)
            st.write("### Investment Advisor Response:")
            st.write(investment_response.content)

        elif "compliance" in user_query.lower():
            with st.spinner("Checking document compliance..."):
                compliance_response = compliance_checker.run({})
            st.write("### Compliance Check Response:")
            st.write(compliance_response.content)

        elif "report" in user_query.lower():
            with st.spinner("Creating a report..."):
                report_response = reporting_agent.run({})
            st.write("### Report:")
            st.write(report_response.content)

        else:
            st.warning("Query not recognized. Please try again with a valid topic.")


if __name__ == "__main__":
    main()